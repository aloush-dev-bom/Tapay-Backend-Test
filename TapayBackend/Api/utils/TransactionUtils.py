"""
Transaction utilities for the API application.
This module contains utility functions for transaction-related operations.
"""

from ..models import Transaction, TransactionHistory, Status


def TrackTransactionChanges(transaction_instance, changes):
    """
    Track changes to a transaction by creating TransactionHistory records.
    
    Args:
        transaction_instance: The Transaction instance being updated
        changes: List of dictionaries with fieldChanged, oldValue, and newValue
        
    Returns:
        list: The created TransactionHistory instances
    """
    history_records = []
    
    for change in changes:
        history = TransactionHistory.objects.create(
            fieldChanged=change["fieldChanged"],
            oldValue=change["oldValue"],
            newValue=change["newValue"],
            transaction=transaction_instance
        )
        history_records.append(history)
    
    return history_records


def UpdateTransactionFields(transaction, data):
    """
    Update transaction fields and track changes.
    
    Args:
        transaction: The Transaction instance to update
        data: Dictionary containing the fields to update
        
    Returns:
        tuple: (updated_transaction, changes_list)
    """
    changes = []
    
    # Update amount if provided
    if "amount" in data:
        old_amount = transaction.amount
        new_amount = data.get("amount")
        if old_amount != new_amount:
            changes.append({
                "fieldChanged": "amount",
                "oldValue": str(old_amount),
                "newValue": str(new_amount)
            })
            transaction.amount = new_amount
    
    # Update payment method if provided
    if "paymentMethod" in data:
        old_method = transaction.paymentMethod
        new_method = data.get("paymentMethod")
        if old_method != new_method:
            changes.append({
                "fieldChanged": "paymentMethod",
                "oldValue": old_method,
                "newValue": new_method
            })
            transaction.paymentMethod = new_method
    
    # Update card number if provided
    if "cardNumber" in data:
        old_card = transaction.cardNumber or ""
        new_card = data.get("cardNumber") or ""
        if old_card != new_card:
            changes.append({
                "fieldChanged": "cardNumber",
                "oldValue": old_card,
                "newValue": new_card
            })
            transaction.cardNumber = new_card
    
    # Update status if provided
    if "status" in data:
        old_status = transaction.transactionStatus.name
        new_status_name = data.get("status")
        
        try:
            new_status = Status.objects.get(name=new_status_name, type="Transaction")
            if old_status != new_status_name:
                changes.append({
                    "fieldChanged": "status",
                    "oldValue": old_status,
                    "newValue": new_status_name
                })
                transaction.transactionStatus = new_status
        except Status.DoesNotExist:
            raise ValueError(f"Status '{new_status_name}' not found")
    
    # Save the transaction if there were changes
    if changes:
        transaction.save()
        TrackTransactionChanges(transaction, changes)
    
    return transaction, changes 