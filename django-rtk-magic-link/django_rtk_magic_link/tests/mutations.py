def request_magic_link_mutation(email, output_values):
    return """mutation {{
        requestMagicLink(
            email: "{email}"
        ) {{
            {output_values}
        }}
    }}""".format(
        email=email,
        output_values=", ".join(output_values),
    )


def sign_in_by_magic_link_mutation(magic_link_token, output_values):
    return """mutation {{
        signInByMagicLink(
            magicLinkToken: "{magic_link_token}"
        ) {{
            {output_values}
        }}
    }}""".format(
        magic_link_token=magic_link_token,
        output_values=", ".join(output_values),
    )
