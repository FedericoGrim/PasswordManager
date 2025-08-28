import { UUID } from "crypto";

export class subAccount {
    Id: UUID;
    Title: string;
    Username: string;
    PasswordEncrypted: string;
    Url: string;
    IdMainUser: UUID;

    constructor(id: UUID, title: string, username: string, passwordEncrypted: string, url: string, user_id: UUID ) {
        this.Id = id;
        this.Title = title;
        this.Username = username;
        this.PasswordEncrypted = passwordEncrypted;
        this.Url = url;
        this.IdMainUser = user_id;
    }
}