
export enum URL {
    ROOT = "/",
    NEWS_BASE = "/news",
    LOGIN = "/login",
    CREATE_ACCOUNT = "/create-account",
    SUBSCRIPTIONS = "/subscription",
    CONFIRM_ACCOUNT = "/confirm-account"
}
export type VALID_PATH = URL.ROOT | URL.NEWS_BASE | URL.LOGIN | URL.CREATE_ACCOUNT | URL.SUBSCRIPTIONS | URL.CONFIRM_ACCOUNT

export class API_KEY {
    static readonly MIXPANEL = "26bbed7c38f303f0108b507263736579"
}