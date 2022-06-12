import { ReactNode } from "react"
import { EmailInput, PasswordInput } from "./FormFields"

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
        "Get the News",
        "",
        "Sign in to your account",
        "Sign in",
        <p className="text-sm text-center text-gray-500">{"No account? "}
            <a className="underline" href="/create-account">Sign up</a>
        </p>
    )
}

function AuthenticationForm(title: string, description: string, formTitle: string, submitButtonText: string, redirectNode: ReactNode ) {
    return (
        <div className="max-w-screen-xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
            <div className="max-w-lg mx-auto">
                <h1 className="text-2xl font-bold text-center text-test-600 sm:text-3xl">{title}</h1>

                <p className="max-w-md mx-auto mt-4 text-center text-grey-500">{description}</p>

                <form action="" className="p-8 mt-6 mb-0 space-y-4 rounded-lg shadow-2xl">
                    <p className="text-lg font-medium">{formTitle}</p>
                    <EmailInput/>
                    <PasswordInput/>
                    <button type="submit" className="block w-full px-5 py-3 text-sm font-medium text-white bg-test-600 rounded-lg">
                        {submitButtonText}
                    </button>
                    {redirectNode}
                </form>
            </div>
        </div>
    )
}