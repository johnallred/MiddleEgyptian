let firstpage = 17;
let lastpage = 419;
let path = 'https://middleegyptian.azurewebsites.net/Search/FaulknerEntries?page=';

describe('Scrape Website', () => {
    for (let i = firstpage; i < lastpage+1; i++) {
        describe(`page${i}`, () => {
            it(`get page`, () => {
                cy.request(`${path}${i}`)
                    .its('body') // NB the response body, not the body of your page
                    .then(content => {
                        cy.writeFile("page" + i + ".json", content);
                    });
            })
        })
    }
})