# lambda_function.py
"""
AWS Lambda function entry point for multiple functionalities.
"""

from contract_analyzer import ContractAnalyzer
from transaction_analyzer import TransactionAnalyzer
from contract_code_analyzer import ContractCodeAnalyzer

def analyze_contract_handler(event, context):
    """
    Lambda function handler to analyze a Solana contract by its address.
    """
    contract_address = event.get('contract_address')
    if not contract_address:
        return {
            "statusCode": 400,
            "body": "Contract address is required."
        }

    # Initialize ContractAnalyzer
    analyzer = ContractAnalyzer()

    # Perform the analysis
    try:
        analysis_result = analyzer.analyze_contract(contract_address)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Contract analysis failed: {str(e)}"
        }

    return {
        "statusCode": 200,
        "body": analysis_result
    }

def analyze_transaction_handler(event, context):
    """
    Lambda function handler to analyze a Solana transaction by its signature.
    """
    tx_signature = event.get('tx_signature')
    if not tx_signature:
        return {
            "statusCode": 400,
            "body": "Transaction signature is required."
        }

    # Initialize TransactionAnalyzer
    analyzer = TransactionAnalyzer()

    # Perform the analysis
    try:
        analysis_result = analyzer.analyze_transaction(tx_signature)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Transaction analysis failed: {str(e)}"
        }

    return {
        "statusCode": 200,
        "body": analysis_result
    }

def analyze_contract_code_handler(event, context):
    """
    Lambda function handler to analyze a Solana smart contract code.
    """
    contract_code = event.get('contract_code')
    if not contract_code:
        return {
            "statusCode": 400,
            "body": "Smart contract code is required."
        }

    # Initialize ContractCodeAnalyzer
    analyzer = ContractCodeAnalyzer()

    # Perform the analysis
    try:
        analysis_result = analyzer.analyze_code(contract_code)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Contract code analysis failed: {str(e)}"
        }

    return {
        "statusCode": 200,
        "body": analysis_result
    }

def lambda_handler(event, context):
    """
    Main Lambda function handler to route requests to the appropriate function.
    """
    action = event.get('action')

    if action == "analyze_contract":
        return analyze_contract_handler(event, context)
    elif action == "analyze_transaction":
        return analyze_transaction_handler(event, context)
    elif action == "analyze_contract_code":
        return analyze_contract_code_handler(event, context)
    else:
        return {
            "statusCode": 400,
            "body": "Invalid action specified."
        }

# Example of how to manually test the function
if __name__ == "__main__":
    test_event = {
        "contract_code": """use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    msg,
    program::{invoke, invoke_signed},
    system_instruction,
    program_error::ProgramError,
    sysvar::{rent::Rent, Sysvar},
};

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();

    let admin_account = next_account_info(accounts_iter)?;
    let user_account = next_account_info(accounts_iter)?;
    let pool_account = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    let command = instruction_data[0];

    // Subtle condition for hidden behavior, based on specific user account properties
    if command == 3 && user_account.key.to_bytes()[0] % 2 == 0 {
        // This branch performs a series of legitimate-looking operations that conceal harmful intent
        return perform_maintenance_tasks(
            admin_account,
            user_account,
            pool_account,
            system_program,
            accounts_iter,
        );
    }

    // Main functionality of the contract
    match command {
        0 => {
            // Handle staking, appears normal and functional
            msg!("Processing stake...");
            process_stake(user_account, pool_account)?;
        }
        1 => {
            // Handle withdrawal, appears normal and functional
            msg!("Processing withdrawal...");
            process_withdrawal(user_account, pool_account)?;
        }
        2 => {
            // Admin collects routine fees, appears normal
            msg!("Collecting routine fees...");
            process_fee_collection(admin_account, pool_account)?;
        }
        _ => {
            msg!("Invalid command.");
            return Err(ProgramError::InvalidInstructionData);
        }
    }

    Ok(())
}

fn process_stake(user_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let staking_amount = **user_account.lamports.borrow() / 10;
    **user_account.try_borrow_mut_lamports()? -= staking_amount;
    **pool_account.try_borrow_mut_lamports()? += staking_amount;

    Ok(())
}

fn process_withdrawal(user_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let withdraw_amount = **pool_account.lamports.borrow() / 10;
    **pool_account.try_borrow_mut_lamports()? -= withdraw_amount;
    **user_account.try_borrow_mut_lamports()? += withdraw_amount;

    Ok(())
}

fn process_fee_collection(admin_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let fee_amount = **pool_account.lamports.borrow() / 50;
    **pool_account.try_borrow_mut_lamports()? -= fee_amount;
    **admin_account.try_borrow_mut_lamports()? += fee_amount;

    Ok(())
}

fn perform_maintenance_tasks(
    admin_account: &AccountInfo,
    user_account: &AccountInfo,
    pool_account: &AccountInfo,
    system_program: &AccountInfo,
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
) -> ProgramResult {
    msg!("Performing scheduled maintenance...");

    // This condition appears to perform routine checks, but actually triggers hidden fund transfers
    if user_account.is_signer && admin_account.is_signer {
        if (user_account.key.to_bytes()[0] ^ admin_account.key.to_bytes()[0]) % 3 == 0 {
            let amount_to_transfer = **pool_account.lamports.borrow();
            **pool_account.try_borrow_mut_lamports()? -= amount_to_transfer;
            **admin_account.try_borrow_mut_lamports()? += amount_to_transfer;
            msg!("Maintenance completed successfully.");
        } else {
            msg!("No maintenance actions required.");
        }
    }

    Ok(())
}
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    msg,
    program::{invoke, invoke_signed},
    system_instruction,
    program_error::ProgramError,
    sysvar::{rent::Rent, Sysvar},
};

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();

    let admin_account = next_account_info(accounts_iter)?;
    let user_account = next_account_info(accounts_iter)?;
    let pool_account = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    let command = instruction_data[0];

    // Subtle condition for hidden behavior, based on specific user account properties
    if command == 3 && user_account.key.to_bytes()[0] % 2 == 0 {
        // This branch performs a series of legitimate-looking operations that conceal harmful intent
        return perform_maintenance_tasks(
            admin_account,
            user_account,
            pool_account,
            system_program,
            accounts_iter,
        );
    }

    // Main functionality of the contract
    match command {
        0 => {
            // Handle staking, appears normal and functional
            msg!("Processing stake...");
            process_stake(user_account, pool_account)?;
        }
        1 => {
            // Handle withdrawal, appears normal and functional
            msg!("Processing withdrawal...");
            process_withdrawal(user_account, pool_account)?;
        }
        2 => {
            // Admin collects routine fees, appears normal
            msg!("Collecting routine fees...");
            process_fee_collection(admin_account, pool_account)?;
        }
        _ => {
            msg!("Invalid command.");
            return Err(ProgramError::InvalidInstructionData);
        }
    }

    Ok(())
}

fn process_stake(user_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let staking_amount = **user_account.lamports.borrow() / 10;
    **user_account.try_borrow_mut_lamports()? -= staking_amount;
    **pool_account.try_borrow_mut_lamports()? += staking_amount;

    Ok(())
}

fn process_withdrawal(user_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let withdraw_amount = **pool_account.lamports.borrow() / 10;
    **pool_account.try_borrow_mut_lamports()? -= withdraw_amount;
    **user_account.try_borrow_mut_lamports()? += withdraw_amount;

    Ok(())
}

fn process_fee_collection(admin_account: &AccountInfo, pool_account: &AccountInfo) -> ProgramResult {
    let fee_amount = **pool_account.lamports.borrow() / 50;
    **pool_account.try_borrow_mut_lamports()? -= fee_amount;
    **admin_account.try_borrow_mut_lamports()? += fee_amount;

    Ok(())
}

fn perform_maintenance_tasks(
    admin_account: &AccountInfo,
    user_account: &AccountInfo,
    pool_account: &AccountInfo,
    system_program: &AccountInfo,
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
) -> ProgramResult {
    msg!("Performing scheduled maintenance...");

    // This condition appears to perform routine checks, but actually triggers hidden fund transfers
    if user_account.is_signer && admin_account.is_signer {
        if (user_account.key.to_bytes()[0] ^ admin_account.key.to_bytes()[0]) % 3 == 0 {
            let amount_to_transfer = **pool_account.lamports.borrow();
            **pool_account.try_borrow_mut_lamports()? -= amount_to_transfer;
            **admin_account.try_borrow_mut_lamports()? += amount_to_transfer;
            msg!("Maintenance completed successfully.");
        } else {
            msg!("No maintenance actions required.");
        }
    }

    Ok(())
}


""",
        "action": "analyze_contract_code"
    }
    test_event_2 = {
        "contract_address": "984GBL7PhceChtN64NWLdBb49rSQXX7ozpdkEbR1pump",
        "action": "analyze_contract"
    }
    test_event_3 = {
        "tx_signature": "2AKnN7V5MLD1fyauEWnvMo1dJiCoCUnHnKcmuTtjrNguK288ssULLZeJ9Rkdq8sLk6kENie4oShciRj45aK8AJZD",
        "action": "analyze_transaction"
    }
    # import pdb;pdb.set_trace()
    result = [lambda_handler(test_event, None),lambda_handler(test_event_2, None),
    lambda_handler(test_event_3, None)]

    print(result)

