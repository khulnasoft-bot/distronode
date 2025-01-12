import { msg, t } from '@lingui/core/macro';
import { Trans } from '@lingui/react/macro';
import ArrowRightIcon from '@patternfly/react-icons/dist/esm/icons/arrow-right-icon';
import { Navigate } from 'react-router-dom';
import {
  distronodeRepositoryCopyAction,
  distronodeRepositoryDeleteAction,
  distronodeRepositoryEditAction,
  distronodeRepositorySyncAction,
} from 'src/actions';
import {
  DistronodeRemoteAPI,
  type DistronodeRemoteType,
  DistronodeRepositoryAPI,
  type DistronodeRepositoryType,
} from 'src/api';
import { PageWithTabs } from 'src/components';
import { Paths, formatPath } from 'src/paths';
import { canViewDistronodeRepositories } from 'src/permissions';
import {
  lastSyncStatus,
  lastSynced,
  parsePulpIDFromURL,
  repositoryBasePath,
} from 'src/utilities';
import { RepositoryAccessTab } from './tab-access';
import { CollectionVersionsTab } from './tab-collection-versions';
import { DetailsTab } from './tab-details';
import { DistributionsTab } from './tab-distributions';
import { RepositoryVersionsTab } from './tab-repository-versions';

const DistronodeRepositoryDetail = PageWithTabs<
  DistronodeRepositoryType & { remote?: DistronodeRemoteType }
>({
  breadcrumbs: ({ name, tab, params: { repositoryVersion, user, group } }) =>
    [
      { url: formatPath(Paths.distronodeRepositories), name: t`Repositories` },
      { url: formatPath(Paths.distronodeRepositoryDetail, { name }), name },
      (tab === 'access' && (group || user)) ||
      (tab === 'repository-versions' && repositoryVersion)
        ? {
            url: formatPath(Paths.distronodeRepositoryDetail, { name }, { tab }),
            name: t`Versions`,
          }
        : null,
      tab === 'access' && group ? { name: t`Group ${group}` } : null,
      tab === 'access' && user ? { name: t`User ${user}` } : null,
      tab === 'repository-versions' && repositoryVersion
        ? { name: t`Version ${repositoryVersion}` }
        : null,
      (tab === 'access' && !user && !group) ||
      (tab === 'repository-versions' && !repositoryVersion)
        ? { name: t`Versions` }
        : null,
    ].filter(Boolean),
  condition: canViewDistronodeRepositories,
  displayName: 'DistronodeRepositoryDetail',
  errorTitle: msg`Repository could not be displayed.`,
  headerActions: [
    distronodeRepositoryEditAction,
    distronodeRepositorySyncAction,
    distronodeRepositoryCopyAction,
    distronodeRepositoryDeleteAction,
  ],
  headerDetails: (item) => (
    <>
      {item?.last_sync_task && (
        <p className='hub-m-truncated'>
          <Trans>Last updated from registry {lastSynced(item)}</Trans>{' '}
          {lastSyncStatus(item)}
        </p>
      )}
    </>
  ),
  listUrl: formatPath(Paths.distronodeRepositories),
  query: ({ name }) => {
    return DistronodeRepositoryAPI.list({ name, page_size: 1 })
      .then(({ data: { results } }) => results[0])
      .then((repository) => {
        // using the list api, so an empty array is really a 404
        if (!repository) {
          return Promise.reject({ response: { status: 404 } });
        }

        const err = (val) => (e) => {
          console.error(e);
          return val;
        };

        return Promise.all([
          repositoryBasePath(repository.name, repository.pulp_href).catch(
            err(null),
          ),
          DistronodeRepositoryAPI.myPermissions(
            parsePulpIDFromURL(repository.pulp_href),
          )
            .then(({ data: { permissions } }) => permissions)
            .catch(err([])),
          repository.remote
            ? DistronodeRemoteAPI.get(parsePulpIDFromURL(repository.remote))
                .then(({ data }) => data)
                .catch(() => null)
            : null,
        ]).then(([distroBasePath, my_permissions, remote]) => ({
          ...repository,
          distroBasePath,
          my_permissions,
          remote,
        }));
      });
  },
  renderTab: (tab, item, actionContext) =>
    ({
      details: <DetailsTab item={item} actionContext={actionContext} />,
      access: <RepositoryAccessTab item={item} actionContext={actionContext} />,
      'collection-versions': (
        <CollectionVersionsTab item={item} actionContext={actionContext} />
      ),
      'repository-versions': (
        <RepositoryVersionsTab item={item} actionContext={actionContext} />
      ),
      distributions: (
        <DistributionsTab item={item} actionContext={actionContext} />
      ),
      collections: (
        <Navigate
          to={formatPath(
            Paths.collections,
            {},
            { repository_name: item?.name },
          )}
        />
      ),
    })[tab],
  tabs: (tab, name) => [
    {
      active: tab === 'details',
      title: t`Details`,
      link: formatPath(
        Paths.distronodeRepositoryDetail,
        { name },
        { tab: 'details' },
      ),
    },
    {
      active: tab === 'access',
      title: t`Access`,
      link: formatPath(
        Paths.distronodeRepositoryDetail,
        { name },
        { tab: 'access' },
      ),
    },
    {
      active: tab === 'collection-versions',
      title: t`Collection versions`,
      link: formatPath(
        Paths.distronodeRepositoryDetail,
        { name },
        { tab: 'collection-versions' },
      ),
    },
    {
      active: tab === 'repository-versions',
      title: t`Versions`,
      link: formatPath(
        Paths.distronodeRepositoryDetail,
        { name },
        { tab: 'repository-versions' },
      ),
    },
    {
      active: tab === 'distributions',
      title: t`Distributions`,
      link: formatPath(
        Paths.distronodeRepositoryDetail,
        { name },
        { tab: 'distributions' },
      ),
    },
    {
      active: tab === 'collections',
      title: t`Collections`,
      icon: <ArrowRightIcon />,
      link: formatPath(Paths.collections, {}, { repository_name: name }),
    },
  ],
});

export default DistronodeRepositoryDetail;
