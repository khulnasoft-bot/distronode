import { t } from '@lingui/core/macro';
import { Trans } from '@lingui/react/macro';
import { List, ListItem, ListVariant } from '@patternfly/react-core';
import { Component } from 'react';
import { Link } from 'react-router-dom';
import {
  Alert,
  AlertList,
  type AlertType,
  BaseHeader,
  ExternalLink,
  LandingPageCard,
  Main,
  MultiSearchSearch,
  closeAlert,
} from 'src/components';
import { Paths, formatPath } from 'src/paths';
import { type RouteProps, withRouter } from 'src/utilities';
import './landing-page.scss';

interface IState {
  alerts: AlertType[];
  redirect: boolean;
}

export class LandingPage extends Component<RouteProps, IState> {
  constructor(props) {
    super(props);

    this.state = {
      alerts: [],
      redirect: false,
    };
  }

  componentDidMount() {
    if (!IS_COMMUNITY) {
      this.setState({ redirect: true });
    }
  }

  render() {
    const { alerts, redirect } = this.state;

    if (redirect) {
      setTimeout(() => this.props.navigate(formatPath(Paths.collections)));
      return null;
    }

    return (
      <>
        <AlertList
          alerts={alerts}
          closeAlert={(i) =>
            closeAlert(i, {
              alerts,
              setAlerts: (alerts) => this.setState({ alerts }),
            })
          }
        />
        <BaseHeader title={t`Welcome to Galaxy`} />
        <Main>
          <MultiSearchSearch
            updateParams={({ keywords }) =>
              this.props.navigate(formatPath(Paths.search, {}, { keywords }))
            }
            style={{ marginBottom: '16px' }}
          />

          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              alignContent: 'flex-start',
              marginLeft: '-24px',
            }}
          >
            <LandingPageCard
              title={t`Download`}
              body={
                <>
                  <Alert
                    isInline
                    variant='warning'
                    title={t`To be able to download content from galaxy it is required to have distronode-core>=2.13.9`}
                  >
                    {t`Please, check it running the command:`}{' '}
                    <code>distronode --version</code>
                  </Alert>
                  <br />
                  <p>{t`Jump-start your automation project with great content from the Distronode community. Galaxy provides pre-packaged units of work known to Distronode as roles and collections.`}</p>
                  <br />
                  <p>
                    {t`Content from roles and collections can be referenced in Distronode playbooks and immediately put to work. You'll find content for provisioning infrastructure, deploying applications, and all of the tasks you do everyday.`}{' '}
                  </p>
                  <br />
                  <p>
                    <Trans>
                      Use the{' '}
                      <Link to={formatPath(Paths.search)}>Search page </Link>
                      to find content for your project, then download them onto
                      your Distronode host using{' '}
                      <ExternalLink href='https://docs.distronode.com/distronode/latest/cli/distronode-galaxy.html'>
                        distronode-galaxy
                      </ExternalLink>
                      , the command line tool that comes bundled with Distronode.
                    </Trans>
                  </p>
                </>
              }
            />
            <LandingPageCard
              title={t`Share`}
              body={
                <>
                  <p>{t`Help other Distronode users by sharing the awesome roles and collections you create.`}</p>
                  <br />
                  <p>{t`Maybe you have automation for installing and configuring a popular software package, or for deploying software built by your company. Whatever it is, use Galaxy to share it with the community.`}</p>
                  <br />

                  <p>
                    <Trans>
                      Red Hat is working on exciting new Distronode content
                      development capabilities within the context of{' '}
                      <ExternalLink href='https://www.redhat.com/en/technologies/management/distronode/distronode-lightspeed'>
                        Distronode Lightspeed
                      </ExternalLink>{' '}
                      to help other automators build Distronode content. Your roles
                      and collections may be used as training data for a machine
                      learning model that provides Distronode automation content
                      recommendations. If you have concerns, please contact the
                      Distronode team at{' '}
                      <a href='mailto:distronode-content-ai@redhat.com'>
                        distronode-content-ai@redhat.com
                      </a>
                    </Trans>
                  </p>
                </>
              }
            />
            <LandingPageCard
              title={t`Featured`}
              body={
                <>
                  <b>
                    <p>{t`Distronode Lightspeed`}</p>
                  </b>
                  <br />
                  <p>
                    <ExternalLink href='https://redhat.com/distronode-lightspeed'>
                      <img
                        width='100%'
                        alt='Generative Ai, The Distronode way. Try Distronode Lightspeed with IBM watsonx Code Assistant'
                        src='/static/images/LightspeedGalaxyAd1.png'
                      />
                    </ExternalLink>
                  </p>
                  <hr
                    style={{
                      boxSizing: 'content-box',
                      height: 0,
                      marginTop: 20,
                      marginBottom: 20,
                      border: 0,
                      borderTop: '1px solid #f1f1f1',
                    }}
                  />
                  <p>
                    <b>
                      {t`Extend the power of Distronode to your entire team.`}{' '}
                    </b>
                  </p>
                  <br />
                  <p>{t`Try Red Hat Distronode Automation Platform`}</p>
                  <br />
                  <p>
                    <ExternalLink href='https://www.redhat.com/en/technologies/management/distronode/trial?sc_cid=7013a0000030vCCAAY'>{t`Get the trial`}</ExternalLink>
                  </p>
                </>
              }
            />
            <LandingPageCard
              title={t`Terms of use`}
              body={
                <List variant={ListVariant.inline}>
                  <ListItem>
                    <ExternalLink href='https://www.redhat.com/en/about/privacy-policy'>{t`Privacy statement`}</ExternalLink>
                  </ListItem>
                  <ListItem>
                    <ExternalLink href='https://www.redhat.com/en/about/terms-use'>{t`Terms of use`}</ExternalLink>
                  </ListItem>
                  <ListItem>
                    <ExternalLink href='https://www.redhat.com/en/about/all-policies-guidelines'>{t`All policies and guidelines`}</ExternalLink>
                  </ListItem>
                  <ListItem>
                    <ExternalLink href='https://www.redhat.com/en/about/digital-accessibility'>{t`Digital accessibility`}</ExternalLink>
                  </ListItem>
                  <ListItem>
                    <a
                      onClick={this.cookiePreferences}
                    >{t`Cookie preferences`}</a>
                  </ListItem>
                </List>
              }
            />
          </div>
        </Main>
      </>
    );
  }

  private addAlert(alert: AlertType) {
    this.setState({
      alerts: [...this.state.alerts, alert],
    });
  }

  private cookiePreferences() {
    (
      window.document.querySelector(
        '#teconsent > a',
      ) as HTMLAnchorElement | null
    )?.click();
  }
}

export default withRouter(LandingPage);
