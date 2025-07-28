output "job_queue_arn" {
  value = aws_batch_job_queue.queue.arn
}

output "job_definition_name" {
  value = aws_batch_job_definition.job.name
}
