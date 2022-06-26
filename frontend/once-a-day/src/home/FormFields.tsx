import { FormEventHandler } from "react"
import { ReactNode, useState } from "react"

export function InputField(inputId: string, placeholder: string, onChange: FormEventHandler, focus: boolean, iconPath?: ReactNode) {
return (
  <div className="py-2">
        <label htmlFor={inputId} className="text-sm font-medium">{inputId[0].toUpperCase() + inputId.substring(1)}</label>
        <div className="relative mt-1">
          <input
            autoFocus={focus}
            type={inputId}
            id={inputId}
            className="w-full p-4 pr-12 text-sm border-test-200 rounded-lg shadow-sm"
            placeholder={placeholder}
            onChange={onChange}
          />
          <span className="absolute inset-y-0 inline-flex items-center right-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-test-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {iconPath}
            </svg>
          </span>
        </div>
      </div>
  )
}

export function EmailInput(onChange: FormEventHandler) {
  return InputField(
    "email",
    "Enter email",
    onChange,
    true,
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
      d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
    />
  )
}

export function PasswordInput(onChange: FormEventHandler) {
    return InputField(
      "password",
      "Enter password",
      onChange,
      false,
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
        />,
    )
}

export function ErrorText(value: string | ReactNode) {
  return (<p className="text-md text-center text-red-500">{value}</p>)
}

export function FormButton(buttonText: string) {
  return (
  <button type="submit" className="block w-full px-5 py-3 text-sm font-medium text-white bg-test-600 rounded-lg">
    {buttonText}
  </button>
  )
}

export function AuthenticationForm(title: string, description: string, formTitle: string, submitButtonText: string, redirectNode: ReactNode, errorMessage: string | undefined, onSubmit: (inputs: Record<string, string>) => void) {
  let [state, setState] = useState({})

  const inputOnChange = (e: React.FormEvent<HTMLInputElement>) => {
    setState({
      // Order is important. Override current state with new update.
      ...state,
      [e.currentTarget.id]: e.currentTarget.value,
    });
  };

  const emailInput = EmailInput(inputOnChange)
  const passwordInput = PasswordInput(inputOnChange)
  

    return FormBox(title, description, (
        <form onSubmit={(e => {e.preventDefault(); onSubmit(state)})}>
          <p className="text-lg font-medium">{formTitle}</p>
          {emailInput}
          {passwordInput}
          {FormButton(submitButtonText)}
          {errorMessage && ErrorText(errorMessage)}
          {redirectNode}
        </form>
    ))
}

export function FormBox(title: string, description: string, child: ReactNode) {
  return (
    <div className="max-w-screen-xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
      <div className="max-w-lg mx-auto">
        <h1 className="text-3xl font-bold text-center text-test-600 sm:text-3xl">{title}</h1>
        <p className="max-w-md mx-auto mt-4 text-center text-grey-500">{description}</p>
        <div className="p-8 mt-6 mb-0 space-y-4 rounded-lg shadow-2xl">
          {child}
        </div>
      </div>
    </div>
  )
}

export function PlanPricingCard(planName: string, planSubtitle: string, monthlyPrice: number, billingFrequency: "Annually" | "Quarterly" | "Monthly", buttonText: string, features: string[], onclick: () => void) {
    return (
        <article className="block p-6 text-center shadow-xl bg-gray-50 rounded-xl">
        <h5 className="text-3xl font-bold text-test-600">{planName}</h5>

        <h6 className="mt-1 text-sm text-gray-900">{planSubtitle}</h6>

        <div className="mt-4 text-gray-900">
            <h6>
            <span className="text-2xl">$</span>
            <span className="inline text-5xl font-bold">{monthlyPrice}</span>
            <span className="text-xs">/ month</span>
            </h6>

            <p className="text-xs text-gray-700 mt-0.5">Billed {billingFrequency}</p>
        </div>

        <ul className="mt-8 space-y-2.5 text-gray-900">
            {features.map((f) => {
                return PricingPlaninclusion(f)
            })}
        </ul>
        <a onClick={onclick}
            className="inline-block px-8 py-3 mt-8 text-sm font-medium text-white transition bg-test-600 rounded hover:bg-test-700 hover:shadow-xl active:bg-test-500 focus:outline-none focus:ring"
        >{buttonText}</a>
        </article>
    )
}

function PricingPlaninclusion(inclusionDescription: string) {
    return (
        <li>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                className="inline w-6 h-6 text-test-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
            >
                <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M5 13l4 4L19 7"
                />
            </svg>
            {inclusionDescription}
            </li>
    )
}