import { ReactNode } from "react"
import { useNavigate } from "react-router-dom";

import { AuthenticationForm, PlanPricingCard } from "./FormFields"

export function CreateAccount() {
    return AuthenticationForm(
        "Get Started Today!",
        "We promise to get you right back to the news",
        "Create an Account",
        "Sign up",
        <p className="text-sm text-center text-gray-500">{"Have an account? "}
            <a className="underline" href="/login">Log in</a>
        </p>
    )
}

export function Login() {
    return AuthenticationForm(
        "news.onceaday.fyi",
        "",
        "Sign in to your account",
        "Sign in",
        <p className="text-sm text-center text-gray-500">{"No account? "}
            <a className="underline" href="/create-account">Sign up</a>
        </p>
    )
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
                        () => {navigate("/create-account")}
                    )}</div>
                    <div className="col-span-1 lg:px-5 my-5">
                    {PlanPricingCard(
                        "Full",
                        "All the news. All the newspapers. Forever.",
                        3, 
                        "Quarterly", 
                        "Select",
                        ["All the news", "All the newspapers"],
                        () => {navigate("/login")}
                    )}</div>
                </div>
                <div className="lg:basis-1/4 xl:basis-1/4"></div>
            </div>
        </div>
    )
}