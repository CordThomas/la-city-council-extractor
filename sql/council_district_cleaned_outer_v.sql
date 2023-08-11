select action_year, action_date,
       trim(replace(
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
                                            replace(
                                              replace(
                                                replace(
                                                  replace(
                                                    replace(
                                                      replace(council,
       'Neughborhood Council', ''),
       '(1st Submittal)', ''),
       '(2nd Submittal)', ''),
       'Hollwood Hills West', 'Hollywood Hills West'),
       'Hollywood Hils West', 'Hollywood Hills West'),
       'Mid City WEST', 'Mid City West'),
       'Los Feliz, Los Feliz', 'Los Feliz'),
       'PICO', 'Pico'),
       'Neighborhood Coucnil', ''),
       'Neigbhorhood Council', ''),
       'Playa Del Rey', 'Playa'),
       'Wilshire Center Koreatown', 'Wilshire Center-Koreatown'),
       'the ', ''),
       'Neighbrohood Council', ''),
       'Mid Town', 'Mid-Town'),
       'Westchester-Playa', 'Westchester/Playa'),
       'Coucnil', ''),
       'Community Impact Statement from by', ''),
       'VIllage', 'Village'),
       'Coun', ''),
       'Neighborhoos cil', ''),
       'United s', '')) as council, file_name
from council_documents_cleaned_inner_2_v