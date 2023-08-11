select action_year, action_date,
      replace(
        replace(
          replace(
            replace(
              replace(
                replace(
                  replace(
                    replace(
                      replace(
                        replace(
                          replace(
                            replace(
                              replace(
                                replace(
                                  replace(
                                    replace(council, 'Community Impact Statement Submitted by ', ''),
                                    'Historic Cultural North,Historic Cultural North', 'Historic Cultural North'),
                                    'neighborhood Council', ''),
                                    'NC', ''),
                                    'Neighborhood Council of', ''),
                                    'Neighborhood Council', ''),
                                    'Neighbhorhood Council', ''),
                                    'United Neighborhoods of the ', ''),
                                    'NDC', ''),
                                    '(EH)', ''),
                                    'Neighborhood', ''),
                                    'Los Feliz,Los Feliz', 'Los Feliz'),
                                    'Foothill Trails District', 'Foothills Trails District'),
                                    'Glassel Park', 'Glassell Park'),
                                    'Neighhborhood Council', ''),
                                    'Neighborhood Development Council', '') as council, file_name
FROM council_documents_cleaned_inner_1_v