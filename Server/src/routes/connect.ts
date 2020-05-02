interface SecretType {
    [key: string]: string;
}

const secrets: SecretType = {
    dbUri: 'mongodb+srv://root:ecoquest2019@ecoquest-3ufot.mongodb.net/ecoquest?retryWrites=true&w=majority'
};

function getSecret(key: string) {
    return secrets[key];
}

export default getSecret;