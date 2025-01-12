const uiPrefix = Cypress.env('uiPrefix');

function clickLightspeedSettings() {
  cy.get('[data-cy="kebab-toggle"] button[aria-label="Actions"]').click({
    force: true,
  });
  cy.contains(
    '[data-cy="kebab-toggle"] a',
    'Distronode Lightspeed settings',
  ).click({
    force: true,
  });
}

describe('Distronode Lightspeed Modal Test', () => {
  before(() => {
    cy.deleteNamespacesAndCollections();
    cy.galaxykit('-i namespace create', 'testns1');
  });

  it('can opt in or opt out of namespace', () => {
    cy.login(null, null, '/', 'Welcome to Galaxy');
    cy.visit(`${uiPrefix}namespaces/testns1`);

    // opt out
    clickLightspeedSettings();
    cy.contains('button', 'Opt out of Distronode Lightspeed').click();
    cy.contains('Namespace testns1 is opted out of Distronode Lightspeed.');

    // opt in
    clickLightspeedSettings();
    cy.contains('button', 'Opt in to Distronode Lightspeed').click();
    cy.contains('Namespace testns1 is opted in to Distronode Lightspeed.');

    clickLightspeedSettings();
    cy.contains('button', 'Opt out of Distronode Lightspeed');
  });
});
