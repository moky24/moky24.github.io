classdef Account < handle
    %ACCOUNT class
    % represents a financial account with a balance, transactions, and goals
    
    properties
        Name
        Balance
        Transactions
        Goals
    end
    
    methods
        % constructor function
        function obj = Account(name, initialBalance) 
            %ACCOUNT Construct an instance of this class
            %   Detailed explanation goes here
            obj.Name = name;
            obj.Balance = initialBalance;
            obj.Transactions = {};
            obj.Goals = {};
        end

        function addIncome(obj, income)
            obj.Balance = obj.Balance + income.Amount;
            %obj.Transactions = [obj.Transactions; income];
            obj.Transactions{end+1} = income;
        end

        function addExpense(obj, expense)
            obj.Balance = obj.Balance - expense.Amount;
            %obj.Transactions = [obj.Transactions; expense]
            obj.Transactions{end+1} = expense;
        end

        function addGoal(obj, goal)
            obj.Goals{end+1} = goal;
        end


        function summary = getSummary(obj)
            % summary of transactions
            summary = obj.Transactions;
        end

        function goalsSummary = getGoalsSummary(obj)
            goalsSummary = obj.Goals;
        end

        %overloaded function
        function disp(obj)
            fprintf('this is %s account, with balance of %4.2f. %s',...
                obj.Name, obj.Balance) % , currencies(currencyOption)
        end
    end
end

