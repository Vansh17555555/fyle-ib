from flask import Blueprint, jsonify, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum

from .schema import AssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    assignment = AssignmentSchema().load(incoming_payload)
    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)

from flask import Blueprint, jsonify, request
from core import db
from core.apis import decorators
from core.models.assignments import Assignment

from .schema import AssignmentSchema

#principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit and grade an assignment"""
    assignment_id = incoming_payload.get('id')
    grade = incoming_payload.get('grade')
    
    # Fetch the assignment using the assignment_id
    assignment = Assignment.query.get(assignment_id)
    
    # Ensure assignment exists
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Check if the assignment is in DRAFT state
    if assignment.state == AssignmentStateEnum.DRAFT:
        return jsonify({'error': 'Assignment in DRAFT state cannot be graded'}), 400

    # Update the assignment's state and grade
    assignment.state = AssignmentStateEnum.GRADED
    assignment.grade = grade

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated assignment
    assignment_dump = AssignmentSchema().dump(assignment)

    # Return the response with the serialized assignment data
    return jsonify({'data': assignment_dump}), 200
