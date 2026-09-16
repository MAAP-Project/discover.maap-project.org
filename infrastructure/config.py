from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppConfig(BaseSettings):
    project_id: str = Field(
        description="Project ID", default="federated-collection-discovery"
    )
    stage: str = Field(description="Stage of deployment", default="test")
    api_version: str = Field(
        description="Version of stac-fastapi-collection-discovery "
        "application to install",
        default="0.1.1",
    )
    stac_api_urls: str = Field(
        description="Comma separated list of STAC API urls to include in the federated "
        "collection discovery app",
        default="",
    )
    api_domain_name: str | None = Field(
        description="Custom domain name for the API endpoint",
        default=None,
    )
    client_domain_name: str | None = Field(
        description="Custom domain name for the client application",
        default=None,
    )
    api_certificate_arn: str | None = Field(
        description="arn for the certificate for the custom domains",
        default=None,
    )
    client_certificate_arn: str | None = Field(
        description="arn for the certificate for the custom domains",
        default=None,
    )
    web_acl_arn: str | None = Field(
        description="arn for the web acl to use for the api",
        default=None,
    )

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.api_certificate_arn is None and self.api_domain_name:
            raise ValueError(
                "If a custom domain is provided for the api, api_certificate_arn must "
                "be provided"
            )

        if (
            self.client_certificate_arn
            and "us-east-1" not in self.client_certificate_arn
        ):
            raise ValueError(
                "client_certificate_arn must be in us-east-1 for use in "
                "CloudFront. The provided certificate is not in us-east-1: "
                f"{self.client_certificate_arn}",
            )

        if self.client_certificate_arn is None and self.client_domain_name:
            raise ValueError(
                "If a custom domain is provided for the client, client_certificate_arn "
                "must be provided"
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env-cdk", yaml_file="config.yaml", extra="allow"
    )
