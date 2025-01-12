import { msg } from '@lingui/core/macro';
import { Paths, formatPath } from 'src/paths';
import { canAddDistronodeRepository } from 'src/permissions';
import { Action } from './action';

export const distronodeRepositoryCreateAction = Action({
  condition: canAddDistronodeRepository,
  title: msg`Add repository`,
  onClick: (item, { navigate }) =>
    navigate(formatPath(Paths.distronodeRepositoryEdit, { name: '_' })),
});
