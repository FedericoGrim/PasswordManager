import { UUID } from "crypto";

export class subAccount {
    id: UUID;
    title: string;
    username: string;
    password: string;
    url: string;
    user_id: UUID;

    constructor(id: UUID, title: string, username: string, password: string, url: string, user_id: UUID ) {
        this.id = id;
        this.title = title;
        this.username = username;
        this.password = password;
        this.url = url;
        this.user_id = user_id;
    }
}