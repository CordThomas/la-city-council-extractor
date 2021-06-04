[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#processing">Processing</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## About The Project

This collection of scripts scans the Los Angeles City Council
File database for all recorded files and extracts information
about each file into a sqlite database for further analysis.

Eventually this will be automated into a daily routine so that
the meta data is up to date.   Post processing on the database
could be used to extract trends on topics of concern, voting
practices of councilmembers and how long various motions take
to make it through the City Council.

It appears that the database dates back to 1998.  There was some
sort of change in the structure of the database in 2008/09. Prior 
to 2009, there was a Subject field that included a summary of the 
file and the list of file activities at the bottom of the page 
is a simple text list vs the list of files and links.  The 
structure appears to have changed around CF 08-2115

The number of council files varies broadly from 1300 in 2018 to
2085 in 2011.  Not all council files are motions by City Councilmembers;
many are administrative files, budget notices, etc.  Of those
involving a motion by a City Councilmember, the frequency of
files ranges from 443 in 2018 to 736 in 2020.

### Built With

This project was built with:

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [urllib](https://pypi.org/project/urllib3/)

## Usage

To process the entire collection of council files, run

python scrape_council_files.py

To process subsets of the council files, edit lines 37 and 39 of 
the scrape_council_files.py scripts

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Cord Thomas - [LinkedIn](https://www.linkedin.com/in/cordthomas/) - cord.thomas@gmail.com

Project Link: [https://github.com/CordThomas/la-city-council-extractor](https://github.com/CordThomas/la-city-council-extractor)

## Processing

The main process script is scrape_council_files.py
* Loops over the history of council files from 2000 through 
  current from teh LA Council File database
* Grabs some summary information from each council file (see 
  data_structures) (scrape_cf_file)
* Grabs some summary information about how the council voted (scrape_cf_votes)
* Grabs the vote results for each motion

## Acknowledgements
* [Dan Kegels Council File Indexer for Community Impact Statements](https://github.com/dankegel/cfindexer)


[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/cordthomas/