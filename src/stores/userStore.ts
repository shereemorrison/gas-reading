import { writable } from 'svelte/store'

export const userLoggedIn = writable<boolean>(false);