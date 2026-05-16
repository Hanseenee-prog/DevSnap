import { Client, Account, Databases, Storage } from 'appwrite';

const client = new Client()
    .setEndpoint("https://fra.cloud.appwrite.io/v1")
    .setProject('6a079a93001afe2b3263');           

export const account = new Account(client);
export const databases = new Databases(client);
export const storage = new Storage(client);
export default client;
