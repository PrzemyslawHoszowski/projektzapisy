Feature: Student wants to create tickets for polls

    Background:
        Given I start new scenario for "grade"    

    Scenario: Student successfully creates tickets for all his polls (with grouping)
        Given the grading protocol is "on"
        And I am signed for groups with polls
        And I am logged in with "student" privileges                        
        And I am on grade main page     
        When I follow "Pobierz bilety"
        And I uncheck "no" checkboxes in tickets grouping options
        And I press "Pobierz bilety"
        Then I wait for a while to see "Pomyślnie wygenerowano bilety"
    
    Scenario: Student successfully creates tickets for all his polls (without grouping) 
        Given the grading protocol is "on"
        And I am signed for groups with polls
        And  I am logged in with "student" privileges       
        And I am on grade main page
        When I follow "Pobierz bilety"
        And I uncheck "all" checkboxes in tickets grouping options
        And I press "Pobierz bilety"
        Then I wait for a while to see "Pomyślnie wygenerowano bilety"
        
    Scenario: Student successfully creates tickets for all his polls (with partial grouping)
        Given the grading protocol is "on"
        And I am signed for groups with polls        
        And I am logged in with "student" privileges    
        And I am on grade main page
        When I follow "Pobierz bilety"
        And I uncheck "some" checkboxes in tickets grouping options
        And I press "Pobierz bilety"        
        Then I wait for a while to see "Pomyślnie wygenerowano bilety"
            
    Scenario: Student fails to create tickets for all his polls - tickets already created
        Given the grading protocol is "on"  
        And I am signed for groups with polls           
        And  I am logged in with "student" privileges   
        And I am on grade main page
        When I follow "Pobierz bilety"
        And I press "Pobierz bilety"
        Then I wait for a while to see "Pomyślnie wygenerowano bilety"
        And I follow "Pobierz bilety"
        And I press "Pobierz bilety"
        Then I wait for a while to see "Nie udało się pobrać następujących biletów:"
        And I should see "Bilet już pobrano"
        
    Scenario: Student tries to create tickets for polls when the protocol is off
        Given the grading protocol is "off" 
        And  I am logged in with "student" privileges   
        And I am on grade main page
        When I go to /grade/ticket/connections_choice
        Then I should see "Ocena zajęć jest w tej chwili zamknięta; nie można pobrać biletów"       