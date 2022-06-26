import { CognitoUser, CognitoUserSession } from "amazon-cognito-identity-js";
import { ReactNode, useState } from "react"
import { useNavigate } from "react-router-dom";

import { AuthenticationForm, ErrorText, FormBox, FormButton, InputField, PlanPricingCard } from "./FormFields"
import UserAPI from "./UserAPI";
import { URL } from "../constants"

let delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export function CreateAccount() {
    let navigate = useNavigate();
    let [err_node, set_err_node] = useState("")

    return AuthenticationForm(
        "Get Started Today!",
        "We promise to get you right back to the news",
        "Create an Account",
        "Sign up",
        <p className="py-3 text-sm text-center text-gray-500">{"Have an account? "}
            <a className="underline" href="/login">Log in</a>
        </p>,
        err_node,
        (input) => {
            UserAPI.createAccount(
                input["email"],
                input["password"],
                (u: CognitoUser) => {navigate(URL.CONFIRM_ACCOUNT)},
                (err: Error) => {set_err_node(err.message)}
            )
        }
    )
}

export function Login() {
    let navigate = useNavigate();
    let [err_node, set_err_node] = useState("")

    return AuthenticationForm(
        "news.onceaday.fyi",
        "",
        "Sign in to your account",
        "Sign in",
        <p className="py-3 text-sm text-center text-gray-500">{"No account? "}
            <a className="underline" href="/create-account">Sign up</a>
        </p>,
        err_node,
        (input) => {
            UserAPI.login(input["email"], input["password"], (_: CognitoUserSession) => {navigate(URL.ROOT)}, (err: Error) => {set_err_node(err.message)})
        }
    )
}

export function ConfirmAccount() {
    let navigate = useNavigate();

    interface ConfirmState {
        "Verification Code": string
        "err_node": string | ReactNode
        disable_resend: boolean
    }
    let [state, setState] = useState<ConfirmState>({"Verification Code": "", "err_node": "", disable_resend: false})


    const inputOnChange = (e: React.FormEvent<HTMLInputElement>) => {
      setState({
        // Order is important. Override current state with new update.
        ...state,
        [e.currentTarget.id]: e.currentTarget.value,
      });
    };

    const submit = () => {
        UserAPI.confirmRegistration(
            state["Verification Code"],
            () => {navigate(URL.SUBSCRIPTIONS)},
            handleError
        )
    }

    const resend = () => {
        // Reduce spamming of emails
        if (state.disable_resend) {return}

        setState({...state, disable_resend: true})
        UserAPI.resendRegistrationCode(() => {}, handleError)
        delay(2000).then(() => {setState({...state, disable_resend: false})})
    }

    const handleError = (e: Error) => {
        if (e.message == "NoUser") {
            setState({...state, err_node: <p className="text-md text-center">Please login, <a className="underline" href="/login">here</a></p>})
        } else {
            setState({...state, err_node: ErrorText(e.message)})
        }
    }

    return FormBox(
        "Check your inbox",
        "We've sent you a verification code to your email", (
        <form onSubmit={(e => {e.preventDefault(); submit()})}>
            {InputField("Verification Code", "Abc123...", inputOnChange)}
            {FormButton("Verify")}
            {state.err_node && state.err_node}
            <p className="py-3 text-sm text-center text-gray-500">{"Didn't receive it? "}
                <a className={!state.disable_resend ? "underline": ""} onClick={resend}>Resend code</a>
            </p>
        </form>
    ))
}

export function SelectSubscription() {
    // TODO: change to route to news page (and login, etc). 
    let navigate = useNavigate();
    const title = "Select an option"
    return  (
        <div>
            <h3 className="block p-6 text-center lg:my-8 text-4xl font-bold text-test-600 justify-center">{title}</h3>
            <div className="flex flex-row justify-center">
                <div className="lg:basis-1/4 xl:basis-1/4"></div>
                <div className="lg:basis-2/4 grid md:grid-cols-1 sm:grid-cols-1 xl:grid-cols-2">
                    <div className="col-span-1 lg:px-5 my-5">
                    {PlanPricingCard(
                        "Free",
                        "No strings attached",
                        0, 
                        "Quarterly", 
                        "Select",
                        ["First point", "Second point"], 
                        () => {navigate(URL.CREATE_ACCOUNT)}
                    )}</div>
                    <div className="col-span-1 lg:px-5 my-5">
                    {PlanPricingCard(
                        "Full",
                        "All the news. All the newspapers. Forever.",
                        3, 
                        "Quarterly", 
                        "Select",
                        ["All the news", "All the newspapers"],
                        () => {navigate(URL.LOGIN)}
                    )}</div>
                </div>
                <div className="lg:basis-1/4 xl:basis-1/4"></div>
            </div>
        </div>
    )
}