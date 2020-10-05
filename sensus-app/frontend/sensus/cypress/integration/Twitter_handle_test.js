describe ("Loads twitter handle",  () => {
    it("loads", () => {
      cy.get(".twitter-handle")
    })
    it("has twitter handle", () => {
        cy.wait(2000)
        cy.get("h1")
            .should("have.value", "textContent", "@realdonaldtrump")
    })
})
