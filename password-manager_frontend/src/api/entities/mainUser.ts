import { UUID } from "crypto";

export class mainUser {
    IdKeycloak: UUID;
    Id: UUID;
    SaltArgon: string;
    HashMasterPassword: string;

    constructor(idKeycloak: UUID, id: UUID, saltArgon: string, hashMasterPassword: string) {
        this.IdKeycloak = idKeycloak;
        this.Id = id;
        this.SaltArgon = saltArgon;
        this.HashMasterPassword = hashMasterPassword;
    }
}