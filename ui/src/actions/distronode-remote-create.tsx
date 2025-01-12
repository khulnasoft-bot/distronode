import { msg } from '@lingui/core/macro';
import { Paths, formatPath } from 'src/paths';
import { canAddDistronodeRemote } from 'src/permissions';
import { Action } from './action';

export const distronodeRemoteCreateAction = Action({
  condition: canAddDistronodeRemote,
  title: msg`Add remote`,
  onClick: (item, { navigate }) =>
    navigate(formatPath(Paths.distronodeRemoteEdit, { name: '_' })),
});
