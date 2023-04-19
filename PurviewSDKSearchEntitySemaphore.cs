using Azure;
using Azure.Analytics.Purview.Catalog;
using Azure.Core;
using DGCM.Purview.Engine.Models;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
namespace DGCM.Purview.Engine.Services {
  public class PurviewService : IPurviewService {
    private readonly PurviewCatalogClient _purviewClient;
    public readonly int MAX_RESULTS_PER_PAGE = 1000;
    public PurviewService(PurviewCatalogClient purviewClient) {
      _purviewClient = purviewClient;
    }
    public async Task<PurviewSearchResult> SearchByKeywords(string keywords,
                                                            int limit = 50,
                                                            int offset = 0) {
      var searchSchema = new PurviewSearchParameters {
        Keywords = keywords,
        Limit = limit,
        Offset = offset,
      };
      var serializedSearchSchema = RequestContent.Create(searchSchema);
      var response = await _purviewClient.SearchAsync(serializedSearchSchema);
      if (response.Status != (int)HttpStatusCode.OK) {
        throw new Exception("Purview's SearchAsync has failed!");
      }
      return await JsonSerializer.DeserializeAsync<PurviewSearchResult>(
          response.Content.ToStream());
    }
    public async Task<PurviewSearchResult> GetAll() {
      var result = await SearchByKeywords("*", MAX_RESULTS_PER_PAGE, 0);
      if (result.SearchCount < MAX_RESULTS_PER_PAGE) {
        return result;
      }
      int remainingPages =
          (int)Math.Ceiling(result.SearchCount / (double)MAX_RESULTS_PER_PAGE) -
          1;  // TODO: Remove this after Purview fixes the offset limit.
      remainingPages = Math.Min(remainingPages, 100);
      var searchTasks =
          (Enumerable.Range(1, remainingPages)).Select(async i => {
            var page = await SearchByKeywords("*", MAX_RESULTS_PER_PAGE,
                                              i * MAX_RESULTS_PER_PAGE);
            result.Value.AddRange(page.Value);
          });
      await Task.WhenAll(searchTasks);
      return result;
    }  /// <inheritdoc/>
    public async Task<PurviewGetByGuidResult> GetEntityById(string id) {
      try {
        var response = await _purviewClient.Entities.GetByGuidAsync(
            id, new RequestOptions());
        return await JsonSerializer.DeserializeAsync<PurviewGetByGuidResult>(
            response.Content.ToStream());
      } catch (RequestFailedException ex) {
        throw new RequestFailedException(
            "Purview's GetByGuidAsync has failed! Does the provided GUID exist?",
            ex);
      }
    }
    public async Task<IEnumerable<PurviewCompleteEntity>> GetAllEnriched(
        Action<string> progressCallback = null, int maxConcurrentTasks = 250) {
      progressCallback("starting Purview search");
      var purviewSearchResult = await GetAll();
      progressCallback(
          $"Purview search done: {purviewSearchResult.Value.Count} results fetched");
      var completeEntities = new ConcurrentBag<PurviewCompleteEntity>();
      using (var semaphore =
                 new SemaphoreSlim(initialCount: maxConcurrentTasks)) {
        int count = 0;
        var t0 = DateTime.Now.TimeOfDay;
        progressCallback("starting GetEntityById");
        ConcurrentBag<Task> tasks = new ConcurrentBag<Task>();
        foreach (var item in purviewSearchResult.Value) {
          semaphore.Wait();
          var t = Task.Factory.StartNew(async () => {
            try {
              var getByIdResult = await GetEntityById(item.Id);
              completeEntities.Add(
                  PurviewCompleteEntity.MergeEntityAndSearchResult(
                      getByIdResult.Entity, item));
            } catch (RequestFailedException) {
              var getByIdResult = new PurviewGetByGuidResult() {
                Entity = new PurviewEntity { Guid = item.Id }
              };
              completeEntities.Add(
                  PurviewCompleteEntity.MergeEntityAndSearchResult(
                      getByIdResult.Entity, item));
            } finally {
              if (count % 100 == 0 && count != 0) {
                progressCallback(
                    $"{count}/{purviewSearchResult.Value.Count} details fetched - {(DateTime.Now.TimeOfDay - t0).TotalSeconds}s");
                t0 = DateTime.Now.TimeOfDay;
              }
              count++;
              semaphore.Release();
            }
          });
          tasks.Add(t);
        }
        await Task.WhenAll(tasks);
      }
      return completeEntities;
    }
  }
}
