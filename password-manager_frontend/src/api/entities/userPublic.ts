// Public lookup shape only — id/username/code/public keys. Never carries
// private_key_*/salt: those must never leave the owning user's own session.
export class userPublic {
    id: string;
    username: string;
    code: string;
    public_key_ec: string;
    public_key_pq: string;

    constructor(fields: { id: string; username: string; code: string; public_key_ec: string; public_key_pq: string }) {
        this.id = fields.id;
        this.username = fields.username;
        this.code = fields.code;
        this.public_key_ec = fields.public_key_ec;
        this.public_key_pq = fields.public_key_pq;
    }
}
