import { msg, t } from '@lingui/core/macro';
import {
  distronodeRemoteDeleteAction,
  distronodeRemoteDownloadCAAction,
  distronodeRemoteDownloadClientAction,
  distronodeRemoteDownloadRequirementsAction,
  distronodeRemoteEditAction,
} from 'src/actions';
import { DistronodeRemoteAPI, type DistronodeRemoteType } from 'src/api';
import { PageWithTabs } from 'src/components';
import { Paths, formatPath } from 'src/paths';
import { canViewDistronodeRemotes } from 'src/permissions';
import { parsePulpIDFromURL } from 'src/utilities';
import { RemoteAccessTab } from './tab-access';
import { DetailsTab } from './tab-details';

const DistronodeRemoteDetail = PageWithTabs<DistronodeRemoteType>({
  breadcrumbs: ({ name, tab, params: { user, group } }) =>
    [
      { url: formatPath(Paths.distronodeRemotes), name: t`Remotes` },
      { url: formatPath(Paths.distronodeRemoteDetail, { name }), name },
      tab === 'access' && (group || user)
        ? {
            url: formatPath(Paths.distronodeRemoteDetail, { name }, { tab }),
            name: t`Access`,
          }
        : null,
      tab === 'access' && group ? { name: t`Group ${group}` } : null,
      tab === 'access' && user ? { name: t`User ${user}` } : null,
      tab === 'access' && !user && !group ? { name: t`Access` } : null,
    ].filter(Boolean),
  condition: canViewDistronodeRemotes,
  displayName: 'DistronodeRemoteDetail',
  errorTitle: msg`Remote could not be displayed.`,
  headerActions: [
    distronodeRemoteEditAction,
    distronodeRemoteDownloadRequirementsAction,
    distronodeRemoteDownloadClientAction,
    distronodeRemoteDownloadCAAction,
    distronodeRemoteDeleteAction,
  ],
  listUrl: formatPath(Paths.distronodeRemotes),
  query: ({ name }) => {
    return DistronodeRemoteAPI.list({ name })
      .then(({ data: { results } }) => results[0])
      .then((remote) => {
        // using the list api, so an empty array is really a 404
        if (!remote) {
          return Promise.reject({ response: { status: 404 } });
        }

        return DistronodeRemoteAPI.myPermissions(
          parsePulpIDFromURL(remote.pulp_href),
        )
          .then(({ data: { permissions } }) => permissions)
          .catch((e) => {
            console.error(e);
            return [];
          })
          .then((my_permissions) => ({ ...remote, my_permissions }));
      });
  },
  renderTab: (tab, item, actionContext) =>
    ({
      details: <DetailsTab item={item} actionContext={actionContext} />,
      access: <RemoteAccessTab item={item} actionContext={actionContext} />,
    })[tab],
  tabs: (tab, name) => [
    {
      active: tab === 'details',
      title: t`Details`,
      link: formatPath(Paths.distronodeRemoteDetail, { name }, { tab: 'details' }),
    },
    {
      active: tab === 'access',
      title: t`Access`,
      link: formatPath(Paths.distronodeRemoteDetail, { name }, { tab: 'access' }),
    },
  ],
});

export default DistronodeRemoteDetail;
