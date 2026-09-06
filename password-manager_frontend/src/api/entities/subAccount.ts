// Every *_encrypted field is an AES-GCM(team key) base64 blob produced by
// encrypt() in Cript-Dectipr.ts — never plaintext on the wire or at rest.
export class subAccount {
    id: string;
    team_id: string;
    username_encrypted: string;
    email_encrypted: string;
    password_encrypted: string;
    site_link_encrypted: string;
    required_perm_level_id: string;

    constructor(fields: {
        id: string;
        team_id: string;
        username_encrypted: string;
        email_encrypted: string;
        password_encrypted: string;
        site_link_encrypted: string;
        required_perm_level_id: string;
    }) {
        this.id = fields.id;
        this.team_id = fields.team_id;
        this.username_encrypted = fields.username_encrypted;
        this.email_encrypted = fields.email_encrypted;
        this.password_encrypted = fields.password_encrypted;
        this.site_link_encrypted = fields.site_link_encrypted;
        this.required_perm_level_id = fields.required_perm_level_id;
    }
}
