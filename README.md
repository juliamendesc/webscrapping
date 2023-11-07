# Web-scrapping with Python

## Description

This is a simple web-scrapping project using Python and BeautifulSoup4. The project is a simple web-scrapping of [LinkedIn](https://www.linkedin.com/jobs/search/) for determined job positions in a determined geolocation. It is possible to search for a job position in a specific city and state, or in a specific city and country. The results are saved in a CSV file that can be later treated to extract the desired information.

## Requirements

All the project's requirements are in the `requirements.txt` file. To install them, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the project, run the following command:

```bash
python3 webscrapper.py
```

If you wish to change the job position, city or state, or city and country, you can change the variables `job_position`, `city` and `state` or `country` in the `webscrapper.py` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authorship

This project was developed with 💜 by [Julia Mendes](https://www.linkedin.com/in/juliamendesc/), following numerous tutorials and guides on the internet, as well as thoroughly consulting the packages official documentation.
