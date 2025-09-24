import { UUID } from "crypto";

export class mainUser {
    IdKeycloak: UUID;
    Id: UUID;
    SaltArgon: string;

    constructor(idKeycloak: UUID, id: UUID, saltArgon: string) {
        this.IdKeycloak = idKeycloak;
        this.Id = id;
        this.SaltArgon = saltArgon;
    }
}