export function EmailInput() {
    return (
        <div>
        <label htmlFor="email" className="text-sm font-medium">Email</label>

        <div className="relative mt-1">
          <input
            autoFocus
            type="email"
            id="email"
            className="w-full p-4 pr-12 text-sm border-test-200 rounded-lg shadow-sm"
            placeholder="Enter email"
          />

          <span className="absolute inset-y-0 inline-flex items-center right-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-5 h-5 text-test-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
              />
            </svg>
          </span>
        </div>
      </div>
    )
}

export function PasswordInput() {
    return (
      <div>
      <label htmlFor="password" className="text-sm font-medium">Password</label>
      <div className="relative mt-1">
        <input
          type="password"
          id="password"
          className="w-full p-4 pr-12 text-sm border-test-200 rounded-lg shadow-sm"
          placeholder="Enter password"
        />

      {/* TODO: Add click handler to toggle between type=password/text above */}
        <span className="absolute inset-y-0 inline-flex items-center right-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-5 h-5 text-test-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
            />
          </svg>
        </span>
      </div>
    </div>
    )
}