describe ("Loads webpage",  () => {
    it("loads webpage", () => {
        cy.visit('http://localhost:3000/')
    })
})

describe ("Interacts login input",  () => {
    it("Finds login input", () => {
        cy.get(".Form-input")
    })

    it("Finds inputs", () => {
        cy.get(".Form-input")
            .type("realdonaldtrump")
            .should("have.value", "realdonaldtrump")
    })
})

describe ("Interacts login button",  () => {
    it("Finds login button", () => {
        cy.get(".Submit-Button")
    })

    it("Logs In", () => {
        cy.contains("Login").click()
    })
})
