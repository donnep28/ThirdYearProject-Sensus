describe ("Loads webpage",  () => {
    it("Correct Url", () => {
        cy.url()
            .should('include', "/Metrics")
    })
})
