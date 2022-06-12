import React from 'react';


interface IProps {
}

interface HomeAppState {
}

export default class HomeApp extends React.Component<IProps, HomeAppState> {
  constructor(props: IProps) {
    super(props)
  }

  render() {
    //   Buttons
    const loginString = "Log in"
    const createAccount = "Create Account"

    const firstTitleLine = "All the News."
    const secondTitleLine = "Once a Day."
    const description = "News from all over the internet. In one place. Gathered once a day"
    return (
        <section className="bg-gray-50">
            <div className="max-w-screen-xl px-4 py-32 mx-auto lg:h-screen lg:items-center lg:flex">
                <div className="max-w-xl mx-auto text-center">
                <h1 className="text-3xl font-extrabold sm:text-5xl">
                    {firstTitleLine}
                    <strong className="font-extrabold text-test-700 sm:block">
                    {secondTitleLine}
                    </strong>
                </h1>

                <p className="mt-4 sm:leading-relaxed sm:text-xl">
                    {description}
                </p>

                <div className="flex flex-wrap justify-center gap-4 mt-8">
                    <a className="block w-full px-12 py-3 text-sm font-medium text-white bg-test-600 rounded shadow sm:w-auto active:bg-test-500 hover:bg-test-700 focus:outline-none focus:ring" href="/create-account">
                    {createAccount}
                    </a>

                    <a className="block w-full px-12 py-3 text-sm font-medium text-test-600 rounded shadow sm:w-auto hover:text-test-700 active:text-test-500 focus:outline-none focus:ring" href="/login">
                    {loginString}
                    </a>
                </div>
                </div>
            </div>
        </section>
    )
  }
}