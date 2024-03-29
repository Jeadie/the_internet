import { FormEventHandler } from "react"
import { ReactNode, useState } from "react"

export function PopupContent(title: string, description: string) {
  return (
    <div className="p-8 bg-white border border-test-100 shadow-lg rounded-2xl" role="alert">
      <div className="items-center sm:flex">
        <p className="mt-3 text-lg font-medium">{title}</p>
      </div>

      <p className="mt-4 text-gray-500">{description}</p>
    </div>
  )
}

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

export function Spinner(className: string) {
  {/* From https://raw.githubusercontent.com/SamHerbert/SVG-Loaders/master/svg-loaders/bars.svg */}
  const size = 38
  const strokeWidth = 5
  const radius = (size/2) - strokeWidth
  const color = "#000"
  return (
    <div className={"flex justify-center items-center " + className}>
      <svg width={size} height={size} viewBox={[0, 0, size+5, size+5].join(" ")} xmlns="http://www.w3.org/2000/svg">
          <defs>
              <linearGradient x1="8.042%" y1="0%" x2="65.682%" y2="23.865%" id="a">
                  <stop stop-color={color} stop-opacity="0" offset="0%"/>
                  <stop stop-color={color} stop-opacity=".631" offset="63.146%"/>
                  <stop stop-color={color} offset="100%"/>
              </linearGradient>
          </defs>
          <g fill="none" fill-rule="evenodd">
              <g transform="translate(7 7)">
                  <path d="M33 14c0-9.94-8.06-14-14-14" id="Oval-2" stroke="url(#a)" stroke-width={strokeWidth}>
                      <animateTransform
                          attributeName="transform"
                          type="rotate"
                          from={[0, radius, radius].join(" ")}
                          to={[360, radius, radius].join(" ")}
                          dur="0.7s"
                          repeatCount="indefinite" />
                  </path>
              </g>
          </g>
      </svg>
    </div>
  )
}

export function FormButton(buttonText: string) {
  return (
    <div>
      <button type="submit" className="block w-full px-5 py-3 text-sm font-medium text-white bg-test-600 rounded-lg">
        {buttonText}
      </button>
    </div>
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

export function Button(onclick: () => void, button_text: string) {
  return <a onClick={onclick}
      className="inline-block px-8 py-3 mt-8 text-sm font-medium text-white transition bg-test-600 rounded hover:bg-test-700 hover:shadow-xl active:bg-test-500 focus:outline-none focus:ring"
      >{button_text}
    </a>
}

export function PlanPricingCard(planName: string, planSubtitle: string, monthlyPrice: number, billingFrequency: "Annually" | "Quarterly" | "Monthly", button: string | ReactNode, features: string[], onclick: () => void) {
    var buttonNode: ReactNode
    if (typeof button == "string") {
        buttonNode = Button(onclick, button)
    } else {
      buttonNode = button
    }
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
                return PricingPlanInclusion(f)
            })}
        </ul>
        {buttonNode}
        </article>
    )
}

export function PricingPlanInclusion(inclusionDescription: string) {
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