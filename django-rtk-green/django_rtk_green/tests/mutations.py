def activate_account_mutation(activation_token, password, output_values):
    return """mutation {{
        activateAccount(
            activationToken: "{activation_token}"
            password: "{password}"
        ) {{
            {output_values}
        }}
    }}""".format(
        activation_token=activation_token,
        password=password,
        output_values=", ".join(output_values),
    )


def register_account_mutation(
    email, accepts_terms, terms_version_accepted, output_values
):
    return """mutation {{
        registerAccount(
            email: "{email}"
            acceptsTerms: {accepts_terms}
            termsVersionAccepted: "{terms_version_accepted}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        accepts_terms="true" if accepts_terms else "false",
        terms_version_accepted=terms_version_accepted,
        output_values=", ".join(output_values),
    )


def request_password_reset_mutation(email, output_values):
    return """mutation {{
        requestPasswordReset(
            email: "{email}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        output_values=", ".join(output_values),
    )


def reset_password_mutation(password_reset_token, password, output_values):
    return """mutation {{
        resetPassword(
            passwordResetToken: "{password_reset_token}"
            password: "{password}"
        ) {{
            {output_values}
        }}
    }}""".format(
        password_reset_token=password_reset_token,
        password=password,
        output_values=", ".join(output_values),
    )


def change_password_mutation(email, password, new_password, output_values):
    return """mutation {{
        changePassword(
            email: "{email}"
            password: "{password}"
            newPassword: "{new_password}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        password=password,
        new_password=new_password,
        output_values=", ".join(output_values),
    )
