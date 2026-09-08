export class mainUser {
    id: string;
    keycloak_id: string;
    username: string;
    code: string;

    salt: string;

    public_key_ec: string;
    private_key_ec: string;

    public_key_pq: string;
    private_key_pq: string;

    team_key_encrypted?: string;

    constructor(fields: {
        id: string;
        keycloak_id: string;
        username: string;
        code: string;
        salt: string;
        public_key_ec: string;
        private_key_ec: string;
        public_key_pq: string;
        private_key_pq: string;
        team_key_encrypted?: string;
    }) {
        this.id = fields.id;
        this.keycloak_id = fields.keycloak_id;
        this.username = fields.username;
        this.code = fields.code;
        this.salt = fields.salt;
        this.public_key_ec = fields.public_key_ec;
        this.private_key_ec = fields.private_key_ec;
        this.public_key_pq = fields.public_key_pq;
        this.private_key_pq = fields.private_key_pq;
        this.team_key_encrypted = fields.team_key_encrypted;
    }
}
