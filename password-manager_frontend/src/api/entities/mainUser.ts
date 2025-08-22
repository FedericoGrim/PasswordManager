export class mainUser {
    IdKeycloak: string;
    Id: string;
    SaltArgon: string;
    HashMasterPassword: string;

    constructor(idKeycloak: string, id: string, saltArgon: string, hashMasterPassword: string) {
        this.IdKeycloak = idKeycloak;
        this.Id = id;
        this.SaltArgon = saltArgon;
        this.HashMasterPassword = hashMasterPassword;
    }
}