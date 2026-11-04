# What counts as a product

Open this when listing a company's products (step 6) or applying the user's corrections (step 11).

## The two tests

A product is something the company sells on its own, to its own audience. Both tests must pass:

1. **It can be bought by itself.** A customer could buy this and nothing else and get something usable. It is sold under its own name: the name a customer buys, signs up for or gets a quote on.
2. **It has its own audience.** The people who evaluate and use it are a distinguishable set, not simply more of the same buyer.

A product usually shows up as its own entry in the site's product navigation, product menu or pricing.

## Label every candidate

| Kind | What it is | Goes where |
| --- | --- | --- |
| product | Passes both tests | Products table |
| feature | A feature, capability, module, add-on or use case: something a product does rather than something bought by name. A capability with a short generic name (Focus, Talent, Align, Analytics, Automation) is a feature unless it has its own page in the product navigation or its own pricing. | Rejected list |
| plan | A pricing tier, edition or bundle (Free, Pro, Enterprise, Premium, Teams) | Rejected list |
| solution | A solution, industry, role or use-case page ("for IT teams", "for healthcare") | Rejected list |
| campaign | An event, report, launch announcement, promotion or programme | Rejected list |

Also never a product: services pages of a product company (onboarding, support plans, training), integrations, and the company's umbrella brand when everything it sells is one product under one name.

List a non-product candidate only when you considered it and decided against it. Never relabel one "product" to fill the list.

## Shape rules

- A company selling one platform has exactly one product, even if the site lists many capabilities.
- List several products only when the company clearly sells distinct offerings, each standing on its own.
- A services company (agency, studio, consultancy, managed service provider) has exactly one product: the service it sells, named after the company, described as that service and who buys it.
- The pricing page is the most honest source: what a customer can buy separately appears as a separate line; what is really a tier appears as a column of the same table.
- At most 15 products. When unsure whether something is a product or a module, leave it out. Never return an empty list for a company whose site says what it sells: fall back to one entry named after the company. Return nothing only when the site is too thin to tell what the company sells at all.

## Applying the user's corrections

The user works at the company, or knows it, and can see what the site cannot: unlaunched products, the internal roadmap, how they actually package and sell. Their correction outranks both the site and the rules above.

- The user decides what counts as a product. If they name several offerings, each one is a product, even when the site presents them as modules of one platform, and even when the user calls them modules. Never collapse offerings the user named into the platform they sit on.
- Every entry after a correction is a product.
- Read the correction as an edit: apply exactly what it asks, keep every earlier entry it does not dispute, return the full list, never a diff.
- A product the user names goes in even if the site never mentions it. Write its description from the user's words (one plain sentence from the name alone if they gave no detail), and leave its page empty unless the site clearly has one.
- If the user states how many products there are, return exactly that many. If the count exceeds the products they named, fill it with the most distinct product-like offerings the site names; never coin a name.
- If the correction is unusable, return the earlier list unchanged and say why.

Edit patterns (earlier list in brackets, the user's words in quotes, the result after the arrow):

- [Beacon] "add Beacon Status" → Beacon, Beacon Status
- [Beacon, Beacon Status] "remove Status" → Beacon
- [Beacon] "it's called Beacon Cloud now" → Beacon Cloud (a rename: keep the description and page)
- [Beacon] "replace this with Beacon Comms and Beacon Reports" → Beacon Comms, Beacon Reports
- [Beacon Suite] "split it into Composer and Reports" → Composer, Reports
- [Composer, Reports] "these are all one product" → one entry, named as the company brands the combined product
- [Beacon] "Composer, Audiences, Reports" (a bare list names products to include) → Beacon, Composer, Audiences, Reports
- [Beacon] "we have two products, you only found one" → Beacon plus the strongest second offering the site names
- [Beacon] "Beacon is the platform; we sell Composer and Reports on it as separate products" → Composer, Reports (do not return Beacon alone because they called it a platform)
- [] "we are a services company, but treat our service as a product" → one entry named after the company, describing the service
- [] "list each service line as its own product: Incident Readiness Audit, Template Writing, Managed Comms" → those three, each described from the site
