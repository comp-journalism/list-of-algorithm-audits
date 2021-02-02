# list-of-algorithm-audits
A continually-updated list of studies from the CSCW 2021 paper, "Problematic Machine Behavior: A Systematic Literature Review of Algorithm Audits"

(Repository is a work-in-progress)

## Definitions

**Algorithm Audit:** an empirical study investigating a public algorithmic system for potential problematic behavior.
* **empirical study**: includes an experiment or analysis (quantitative or qualitative) that generates evidence-based claims with well-defined outcome metrics. It must not be purely an opinion/position paper, although position papers with substantial empirical components were included
* **algorithmic system**:  is any socio-technical system influenced by at least one algorithm. This includes systems that may rely on human judgement and/or other non-algorithmic components, as long as they include at least one algorithm.
* **public**: algorithmic system is one used in a commercial context or other public setting such as law enforcement, education, criminal justice, or public transportation
* **problematic behavior**: in this study refers to discrimination, distortion, exploitation, or mis- judgement, as well as various types of behaviors within each of these categories. A behavior is problematic when it causes harm (or potential harm). In the ACM Code of Ethics, examples of harm include "unjustified physical or mental injury, unjustified destruction or disclosure of information, and unjustified damage to property, reputation, and the environment."

### Discrimination
The algorithm disparately treats or disparately impacts people on the basis of their race, age, gender, location, socioeconomic status, and/or intersectional identity. For example, an algorithm implicated in discrimination may systematically favor people who identify as males, or reinforce harmful stereotypes about elderly people.
Pricing
* [Detecting price and search discrimination on the internet](https://doi.org/10.1145/2390231.2390245) (Mikians et al., 2012)
* [Crowd-assisted search for price discrimination in E-commerce: First results](https://doi.org/10.1145/2535372.2535415) (Mikians et al., 2013)
* [Measuring Price Discrimination and Steering on E-commerce Web Sites](https://doi.org/10.1145/2663716.2663744) (Hannak et al., 2014)
* [An Empirical Analysis of Algorithmic Pricing on Amazon Marketplace](https://doi.org/10.1145/2872427.2883089) (Chen et al., 2016)
* [An Empirical Study on Online Price Differentiation](https://doi.org/10.1145/3176258.3176338) (Hupperich et al., 2018)
Advertising
* [Discrimination in Online Ad Delivery](https://doi.org/10.1145/2460276.2460278) (Sweeney, 2013)
* [Algorithmic bias? An empirical study of apparent gender-based discrimination in the display of stem career ads](https://doi.org/10.1287/mnsc.2018.3093) (Lambrecht and Tucker, 2019)
* [Auditing Race and Gender Discrimination in Online Housing Market](https://ojs.aaai.org/index.php/ICWSM/article/view/7276) (Asplund et al., 2020)
Search
* [Google search: Hyper-visibility as a means of rendering black women and girls invisible](https://www.proquest.com/docview/1771536966) (Noble, 2013)
* [Unequal Representation and Gender Stereotypes in Image Search Results for Occupations](https://doi.org/10.1145/2702123.2702520) (Kay et al., 2015)
* [Bias in Online freelance marketplaces: Evidence from TaskRabbit and Fiverr](https://doi.org/10.1145/2998181.2998327) (Hannak et al., 2017)
* [Investigating the impact of gender on rank in resume search engines](https://doi.org/10.1145/3173574.3174225) (Chen et al., 2018)
* [Fairness-aware ranking in search & recommendation systems with application to linkedin talent search](https://doi.org/10.1145/3292500.3330691) (Geyik, Ambler, and Kenthapadi, 2019)
Recommendation
* [Tracking gendered streams](https://doi.org/10.3384/cu.2000.1525.1792163) (Eriksson and Johansson, 2017)
Vision
* [Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification](http://proceedings.mlr.press/v81/buolamwini18a.html) (Buolamwini and Gebru, 2018)
* [Actionable auditing: Investigating the impact of publicly naming biased performance results of commercial AI products](https://doi.org/10.1145/3306618.3314244) (Raji and Buolamwini, 2019)
* [Does Object Recognition Work for Everyone?](https://arxiv.org/abs/1906.02659) (DeVries et al., 2019)
* [Fairness in proprietary image tagging algorithms: A cross-platform audit on people images](https://ojs.aaai.org/index.php/ICWSM/article/view/3232) (Kyriakou et al., 2019)
* [Social B(eye)as: Human and machine descriptions of people images](https://ojs.aaai.org/index.php/ICWSM/article/view/3255) (Barlas et al., 2019)
Criminal Justice
* [Why machine learning may lead to unfairness: Evidence from risk assessment for juvenile justice in Catalonia](https://doi.org/10.1145/3322640.3326705) (Tolan et al., 2019)
Language Processing
* [The Risk of Racial Bias in Hate Speech Detection](https://doi.org/10.18653/v1/P19-1163) (Sap et al., 2020)

### Distortion
The algorithm presents media that distorts or obscures an underlying reality. For example, an algorithm implicated in distortion may favor content from a given political perspective, hyper-personalize output for different users, change its output frequently and without good reason, or provide misleading information to users.
Search
* [Measuring Personalization of Web Search](https://doi.org/10.1145/2488388.2488435) (Hannak et al., 2013)
* [Location, Location, Location: The Impact of Geolocation on Web Search Personalization](https://doi.org/10.1145/2815675.2815714) (Kliman-Silver et al., 2015)
* ["Be careful; Things can be worse than they appear" - Understanding biased algorithms and users' behavior around them in rating platforms](https://ojs.aaai.org/index.php/ICWSM/article/view/14898) (Eslami et al., 2017)
* [Quantifying search bias: Investigating sources of bias for political searches in social media](https://doi.org/10.1145/2998181.2998321) (Kulshrestha et al., 2017)
* [From ranking algorithms to ‘ranking cultures’: Investigating the modulation of visibility in YouTube search results](https://doi.org/10.1177/1354856517736982) (Rieder, Matamoros-Fernández, and Coromina, 2018)
* [Challenging Google Search filter bubbles in social and political information: Disconforming evidence from a digital methods case study](https://doi.org/10.1016/j.tele.2018.07.004) (Courtois, Slechten, and Coenen, 2018)
* [Search bias quantification: investigating political bias in social media and web search](https://doi.org/10.1007/s10791-018-9341-2) (Kulshrestha et al., 2018)
* [Auditing partisan audience bias within Google search](https://doi.org/10.1145/3274417) (Robertson et al., 2018)
* [Beyond the bubble: Assessing the diversity of political search results](https://doi.org/10.1080/21670811.2018.1539626) (Puschmann, 2018)
* [You Can’t See What You Can’t See: Experimental Evidence for How Much Relevant Information May Be Missed Due to Google’s Web Search Personalisation](https://doi.org/10.1007/978-3-030-34971-4_17) (Lai and Luczak-Roesch, 2019)
* [Search media and elections: A longitudinal investigation of political search results in the 2018 U.S. Elections](https://doi.org/10.1145/3359231) (Metaxa et al., 2019)
* [Search as news curator: The role of Google in shaping attention to news information](https://doi.org/10.1145/3290605.3300683) (Trielli and Diakopoulos, 2019)
* [Dr. Google, what can you tell me about homeopathy? Comparative study of the top10 websites in the United States, United Kingdom, France, Mexico and Spain](https://doi.org/10.3145/epi.2019.mar.13) (Cano-Orón, 2019)
* [Comparing Platform “Ranking Cultures” Across Languages: The Case of Islam on YouTube in Scandinavia](https://doi.org/10.1177/2056305118817038) (Moe, 2019)
* [Auditing the partisanship of Google search snippets](https://doi.org/10.1145/3308558.3313654) (Hu et al., 2019)
* [Auditing autocomplete: Suggestion networks and recursive algorithm interrogation](https://doi.org/10.1145/3292522.3326047) (Robertson et al., 2019)
* [Auditing local news presence on Google News](https://doi.org/10.1038/s41562-020-00954-0) (Fischer et al., 2020)
* [Measuring Misinformation in Video Search Platforms: An Audit Study on YouTube](https://doi.org/10.1145/3392854) (Hussein et al., 2020)
Mapping
* [MapWatch: Detecting and monitoring international border personalization on online maps](https://doi.org/10.1145/2872427.2883016) (Soeller et al., 2016)
Recommendation
* [More of the same - On spotify radio](https://doi.org/10.3384/cu.2000.1525.1792) (Snickars, 2017)
* [Coding the News: The role of computer code in filtering and distributing news](https://doi.org/10.1080/21670811.2017.1366865) (Weber and Kosterich, 2018)
* [Are We Exposed to the Same “News” in the News Feed?: An empirical analysis of filter bubbles as information similarity for Danish Facebook users](https://doi.org/10.1080/21670811.2018.1510741) (Bechmann and Nielbo, 2018)
* [Analyzing the news coverage of personalized newspapers](https://doi.org/10.1109/ASONAM.2018.8508812) (Chakraborty and Ganguly, 2018)
* [Opening Up the Black Box: Auditing Google’s Top Stories Algorithm](https://par.nsf.gov/biblio/10101277) (Lurie and Mustafaraj, 2019)
* [Auditing radicalization pathways on YouTube](https://doi.org/10.1145/3351095.3372879) (Ribeiro et al., 2020)
* [Auditing News Curation Systems: A Case Study Examining Algorithmic and Editorial Logic in Apple News](https://ojs.aaai.org/index.php/ICWSM/article/view/7277) (Bandy and Diakopoulos, 2020)
Advertising
* [Investigating Ad Transparency Mechanisms in Social Media: A Case Study of Facebook's Explanations](https://dx.doi.org/10.14722/ndss.2018.23204) (Andreou et al., 2018)
* [Ad Delivery Algorithms: The Hidden Arbiters of Political Messaging](https://arxiv.org/abs/1912.04255) (Ali et al., 2019)
Language Processing
* [Bias misperceived: The role of partisanship and misinformation in YouTube comment moderation](https://ojs.aaai.org/index.php/ICWSM/article/view/3229) (Jiang, Robertson, and Wilson, 2019)



### Exploitation
The algorithm inappropriately uses content from other sources and/or sensitive personal information from people. For example, an algorithm implicated in exploitation may infer sensitive personal information from users without proper consent, or feature content from an outside source without attribution.

Advertising
* [Automated Experiments on Ad Privacy Settings](https://doi.org/10.1515/popets-2015-0007) (Datta et al., 2015)
* [Studying ad targeting with digital methods: The case of spotify](https://doi.org/10.3384/cu.2000.1525.1792212) (Mahler and Vonderau, 2017)
* [Unveiling and Quantifying Facebook Exploitation of Sensitive Personal Data for Advertising Purposes](https://dl.acm.org/doi/abs/10.5555/3277203.3277240) (Cabanas, Cuevas, and Cuevas, 2018)
Search
* [The Substantial Interdependence of Wikipedia and Google: A Case Study on the Relationship Between Peer Production Communities and Information Technologies](https://ojs.aaai.org/index.php/ICWSM/article/view/14883) (McMahon, Johnson, and Hecht, 2017)
* [Measuring the Importance of User-Generated Content to Search Engines](https://ojs.aaai.org/index.php/ICWSM/article/view/3248) (Vincent et al., 2019)



### Misjudgement
The algorithm makes incorrect predictions or classifications. Notably, mijudgement can often lead to discrimination, distortion, and/or exploitation, but some studies in the review focused on this initial error of misjudgement without exploring second-order problematic effects. An algorithm implicated in misjudgement may incorrectly classify a user’s employment status or mislabel a piece of political news as being primarily about sports, for example.

Criminal Justice
* [Out With the Old and in With the New? An Empirical Comparison of Supervised Learning Algorithms to Predict Recidivism](https://doi.org/10.1177%2F0887403415604899) (Duwe and Kim, 2017)
* [Better Practices in the Development and Validation of Recidivism Risk Assessments: The Minnesota Sex Offender Screening Tool–4](https://doi.org/10.1177%2F0887403417718608) (Duwe, 2019)
* [The right to confront your accusers: Opening the black box of forensic DNA software](https://doi.org/10.1145/3306618.3314279) (Matthews et al., 2019)
Advertising
* [The Accuracy of the Demographic Inferences Shown on Google's Ad Settings](https://doi.org/10.1145/3267323.3268962) (Tschantz et al., 2018)
* [Auditing Offline Data Brokers via Facebook's Advertising Platform](https://doi.org/10.1145/3308558.3313666) (Venkatadri, 2019)
* [Quantity vs. Quality: Evaluating User Interest Profiles Using Ad Preference Managers](https://doi.org/10.14722/ndss.2019.23392) (Bashir et al., 2019)
* [Facebook Ads Monitor: An Independent Auditing System for Political Ads on Facebook](https://doi.org/10.1145/3366423.3380109) (Silva et al., 2020)
