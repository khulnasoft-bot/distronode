import {
  type FeatureFlagsType,
  type SettingsType,
  type UserType,
} from 'src/api';

export type PermissionContextType = (
  o: {
    featureFlags: FeatureFlagsType;
    settings?: SettingsType;
    user: UserType;
    hasPermission: (string) => boolean;
    hasObjectPermission?: (string, item?) => boolean;
  },
  item?,
) => boolean;

export const isLoggedIn: PermissionContextType = ({ user }) =>
  user && !user.is_anonymous;

const has_model_perms =
  (permission: string): PermissionContextType =>
  ({ hasPermission, user }) =>
    hasPermission(permission) || user?.is_superuser;

const has_model_or_obj_perms =
  (permission: string): PermissionContextType =>
  ({ hasPermission, hasObjectPermission, user }, item?) =>
    hasPermission(permission) ||
    hasObjectPermission?.(permission, item) ||
    user?.is_superuser;

// Distronode Remotes
export const canAddDistronodeRemote = has_model_perms(
  'distronode.add_collectionremote',
);
export const canDeleteDistronodeRemote = has_model_or_obj_perms(
  'distronode.delete_collectionremote',
);
export const canEditDistronodeRemote = has_model_or_obj_perms(
  'distronode.change_collectionremote',
);
export const canViewDistronodeRemotes = has_model_or_obj_perms(
  'distronode.view_collectionremote',
);
export const canEditDistronodeRemoteAccess = has_model_or_obj_perms(
  'distronode.manage_roles_collectionremote',
);

// Distronode Repositories
export const canAddDistronodeRepository = has_model_perms(
  'distronode.add_distronoderepository',
);
export const canDeleteDistronodeRepository = has_model_or_obj_perms(
  'distronode.delete_distronoderepository',
);
export const canEditDistronodeRepository = has_model_or_obj_perms(
  'distronode.change_distronoderepository',
);
export const canSyncDistronodeRepository = canEditDistronodeRepository;
// everybody can list/view, not has_model_or_obj_perms('distronode.view_distronoderepository'); under feature flag
export const canViewDistronodeRepositories = ({ user, featureFlags }) =>
  user && featureFlags?.display_repositories;
export const canEditDistronodeRepositoryAccess = has_model_or_obj_perms(
  'distronode.manage_roles_distronoderepository',
);

// Distronode Repository Versions
// simulating has_repository_model_or_obj_perms by passing in repository as item
export const canRevertDistronodeRepositoryVersion = canEditDistronodeRepository;
