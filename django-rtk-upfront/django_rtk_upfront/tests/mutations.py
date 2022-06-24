def activate_account_mutation(activation_token, output_values):
    return """mutation {{
        activateAccount(
            activationToken: "{activation_token}"
        ) {{
            {output_values}
        }}
    }}""".format(
        activation_token=activation_token,
        output_values=", ".join(output_values),
    )


def register_account_mutation(
    email, password, accepts_terms, terms_version_accepted, output_values
):
    return """mutation {{
        registerAccount(
            email: "{email}"
            password: "{password}"
            acceptsTerms: {accepts_terms}
            termsVersionAccepted: "{terms_version_accepted}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        password=password,
        accepts_terms="true" if accepts_terms else "false",
        terms_version_accepted=terms_version_accepted,
        output_values=", ".join(output_values),
    )


def register_account_with_username_mutation(
    email, username, password, accepts_terms, terms_version_accepted, output_values
):
    return """mutation {{
        registerAccount(
            email: "{email}"
            username: "{username}"
            password: "{password}"
            acceptsTerms: {accepts_terms}
            termsVersionAccepted: "{terms_version_accepted}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        username=username,
        password=password,
        accepts_terms="true" if accepts_terms else "false",
        terms_version_accepted=terms_version_accepted,
        output_values=", ".join(output_values),
    )
