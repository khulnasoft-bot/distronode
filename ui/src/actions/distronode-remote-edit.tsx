import { msg } from '@lingui/core/macro';
import { Paths, formatPath } from 'src/paths';
import { canEditDistronodeRemote } from 'src/permissions';
import { Action } from './action';

export const distronodeRemoteEditAction = Action({
  condition: canEditDistronodeRemote,
  title: msg`Edit`,
  onClick: ({ name }, { navigate }) =>
    navigate(formatPath(Paths.distronodeRemoteEdit, { name })),
});
