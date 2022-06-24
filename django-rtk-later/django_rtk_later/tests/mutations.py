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


def activate_account_with_username_mutation(
    activation_token, password, username, output_values
):
    return """mutation {{
        activateAccount(
            activationToken: "{activation_token}"
            password: "{password}"
            username: "{username}"
        ) {{
            {output_values}
        }}
    }}""".format(
        activation_token=activation_token,
        password=password,
        username=username,
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
