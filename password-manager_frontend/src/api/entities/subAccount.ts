import { UUID } from "crypto";

export class subAccount {
    id: UUID;
    title: string;
    username: string;
    password_encrypted: string;
    url: string;
    user_id: UUID;

    constructor(id: UUID, title: string, username: string, passwordEncrypted: string, url: string, user_id: UUID ) {
        this.id = id;
        this.title = title;
        this.username = username;
        this.password_encrypted = passwordEncrypted;
        this.url = url;
        this.user_id = user_id;
    }
}