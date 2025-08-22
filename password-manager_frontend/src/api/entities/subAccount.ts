export class subAccount {
    Id: string;
    Title: string;
    Username: string;
    PasswordEncrypted: string;
    Url: string;
    IdMainUser: string;

    constructor(id: string, title: string, username: string, passwordEncrypted: string, url: string, idMainUser: string) {
        this.Id = id;
        this.Title = title;
        this.Username = username;
        this.PasswordEncrypted = passwordEncrypted;
        this.Url = url;
        this.IdMainUser = idMainUser;
    }
}