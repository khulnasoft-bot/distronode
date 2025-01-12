import { msg, t } from '@lingui/core/macro';
import { Td, Tr } from '@patternfly/react-table';
import { Link } from 'react-router-dom';
import {
  distronodeRemoteCreateAction,
  distronodeRemoteDeleteAction,
  distronodeRemoteDownloadCAAction,
  distronodeRemoteDownloadClientAction,
  distronodeRemoteDownloadRequirementsAction,
  distronodeRemoteEditAction,
} from 'src/actions';
import { DistronodeRemoteAPI, type DistronodeRemoteType } from 'src/api';
import { CopyURL, ListItemActions, ListPage } from 'src/components';
import { Paths, formatPath } from 'src/paths';
import { canViewDistronodeRemotes } from 'src/permissions';
import { parsePulpIDFromURL } from 'src/utilities';

const listItemActions = [
  // Edit
  distronodeRemoteEditAction,
  // Download requirements.yaml
  distronodeRemoteDownloadRequirementsAction,
  // Download client certificate
  distronodeRemoteDownloadClientAction,
  // Download CA certificate
  distronodeRemoteDownloadCAAction,
  // Delete
  distronodeRemoteDeleteAction,
];

const DistronodeRemoteList = ListPage<DistronodeRemoteType>({
  condition: canViewDistronodeRemotes,
  defaultPageSize: 10,
  defaultSort: '-pulp_created',
  displayName: 'DistronodeRemoteList',
  errorTitle: msg`Remotes could not be displayed.`,
  filterConfig: () => [
    {
      id: 'name__icontains',
      title: t`Remote name`,
    },
  ],
  headerActions: [distronodeRemoteCreateAction], // Add remote
  listItemActions,
  noDataButton: distronodeRemoteCreateAction.button,
  noDataDescription: msg`Remotes will appear once created.`,
  noDataTitle: msg`No remotes yet`,
  query: ({ params }) => DistronodeRemoteAPI.list(params),
  renderTableRow(item: DistronodeRemoteType, index: number, actionContext) {
    const { name, pulp_href, url } = item;
    const id = parsePulpIDFromURL(pulp_href);

    const kebabItems = listItemActions.map((action) =>
      action.dropdownItem({ ...item, id }, actionContext),
    );

    return (
      <Tr key={index}>
        <Td>
          <Link to={formatPath(Paths.distronodeRemoteDetail, { name })}>
            {name}
          </Link>
        </Td>
        <Td>
          <CopyURL url={url} />
        </Td>
        <ListItemActions kebabItems={kebabItems} />
      </Tr>
    );
  },
  sortHeaders: [
    {
      title: msg`Remote name`,
      type: 'alpha',
      id: 'name',
    },
    {
      title: msg`URL`,
      type: 'alpha',
      id: 'url',
    },
  ],
  title: msg`Remotes`,
});

export default DistronodeRemoteList;
