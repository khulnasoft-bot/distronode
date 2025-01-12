import { t } from '@lingui/core/macro';
import { DistronodeRepositoryAPI } from 'src/api';
import { parsePulpIDFromURL } from './parse-pulp-id';
import { waitForTaskUrl } from './wait-for-task';

export async function repositoryRemoveCollection(
  repoName,
  collectionVersion_pulp_href,
  repoHref = null,
) {
  if (!repoHref) {
    repoHref = (
      await DistronodeRepositoryAPI.list({ name: repoName, page_size: 1 })
    )?.data?.results?.[0]?.pulp_href;
  }

  if (!repoHref) {
    return Promise.reject({ error: t`Repository ${repoName} not found.` });
  }

  const task = (
    await DistronodeRepositoryAPI.removeContent(
      parsePulpIDFromURL(repoHref),
      collectionVersion_pulp_href,
    )
  )?.data?.task;

  await waitForTaskUrl(task);
}
