import { msg } from '@lingui/core/macro';
import { Paths, formatPath } from 'src/paths';
import { canEditDistronodeRepository } from 'src/permissions';
import { Action } from './action';

export const distronodeRepositoryEditAction = Action({
  condition: canEditDistronodeRepository,
  title: msg`Edit`,
  onClick: ({ name }, { navigate }) =>
    navigate(formatPath(Paths.distronodeRepositoryEdit, { name })),
});
