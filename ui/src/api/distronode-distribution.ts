import { PulpAPI } from './pulp';

class API extends PulpAPI {
  apiPath = 'distributions/distronode/distronode/';

  // list(params?)
  // delete(pk)
}

export const DistronodeDistributionAPI = new API();
